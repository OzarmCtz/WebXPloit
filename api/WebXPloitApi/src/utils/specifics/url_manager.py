# cython: language_level=3

import re
import asyncio
import src.utils.generics.generic as UtilsGenerics
from pydantic import BaseModel
from fastapi import HTTPException
from tortoise.models import Model
from tortoise import fields
from config.params import ConfigApiConst
from src.vulnerability.disclosure.git.dump_process import VulnDumpProcess

class DbUrl(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=200)
    vuln = fields.CharField(max_length=200)

class UrlRequest(BaseModel):
    url: str
    vuln: str

class DbUrlResponse(BaseModel):
    id: int
    url: str
    vuln: str

class URLManager:
    def __init__(self):
        self.max_workers = ConfigApiConst.LaunchApiConfig.THREADS_API
        self.logger_url_manager = UtilsGenerics.setup_logging(
            logger_name=f"{ConfigApiConst.LoggingApiConfig.LOGGER_OUTPUT_NAME}",
            log_file=ConfigApiConst.LoggingApiConfig.OUTPUT_FILE_PATH,
        )
        self.logger_url_manager.debug("URLManager Init")
        self.git_process = VulnDumpProcess()
        self.regex = self._compile_regex()
        self.threads_api = ConfigApiConst.LaunchApiConfig.THREADS_API

    @staticmethod
    def _compile_regex() -> re.Pattern:
        regex_pattern = (
            r"^(?:http|ftp)s?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
            r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$"
        )
        return re.compile(regex_pattern, re.IGNORECASE)

    async def traitement_url(self, url):
        if url.vuln == 'git-dumper':
            self.logger_url_manager.info(f"{url.url} sent to VulnDumpProcess")
            await self.git_process.run(url.url)
        else:
            self.logger_url_manager.warning(f"{url.url} not sent because {url.vuln} doesn't exist")

    async def url_deleting_controller(self, delete_request: UrlRequest):
        try:
            urls_to_delete_query = DbUrl.filter(url=delete_request.url)
            deleted_count = await urls_to_delete_query.delete()
            if deleted_count:
                self.logger_url_manager.info(
                    f"URL deleted in DB: {delete_request.url}, {deleted_count} times"
                )
                return {"status": "success", "message": f"{deleted_count} URL(s) successfully deleted"}
            else:
                self.logger_url_manager.debug(f"No URL found to delete: {delete_request.url}")
                return {"status": "warning", "message": "No URL found to delete"}
        except Exception as e:
            self._log_and_raise_error(f"Error deleting URL: {e}", 500)

    async def url_adding_controller(self, git_in: UrlRequest):
        url = git_in.url.strip()
        vuln = git_in.vuln.strip()
        
        if not url or not vuln:
            self._log_and_raise_error("The URL or Vuln must not be empty.", 400)

        existing_url = await DbUrl.filter(url=url).first()
        if existing_url:
            return {"status": "warning", "message": "URL already exists in the database"}
        
        try:
            url_added = await DbUrl.create(url=url, vuln=vuln)
            self.logger_url_manager.info(f"URL added to DB: {url_added.url} for vuln: {url_added.vuln}")
            return DbUrlResponse(id=url_added.id, url=url_added.url, vuln=url_added.vuln)
        except Exception as e:
            self._log_and_raise_error(f"Internal Server Error in url_adding_controller: {e}", 500)

    def _log_and_raise_error(self, message: str, status_code: int):
        self.logger_url_manager.debug(message)
        raise HTTPException(status_code=status_code, detail=message)

    async def fetch_urls(self, limit: int = None):
        if limit is None or limit < 0:
            return await DbUrl.all()
        return await DbUrl.all().limit(limit)
    
    async def worker(self, url_queue, semaphore):
        while True:
            url = await url_queue.get()
            if url is None:
                break
            async with semaphore:
                await self.traitement_url(url)

    async def process_urls(self):
        semaphore = asyncio.Semaphore(3)
        url_queue = asyncio.Queue()
        await asyncio.sleep(30)
        [asyncio.create_task(self.worker(url_queue, semaphore)) for _ in range(3)]

        while True:
            try:
                url_objects = await self.fetch_urls(limit=3)
                if not url_objects:
                    await asyncio.sleep(30)
                    continue

                for url_obj in url_objects:
                    url_request = UrlRequest(url=url_obj.url, vuln=url_obj.vuln)
                    await self.url_deleting_controller(url_request)
                    await url_queue.put(url_obj)

            except Exception as e:
                print(f"Error processing URLs: {e}")
                await asyncio.sleep(30)
