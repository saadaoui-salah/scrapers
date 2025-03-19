from scrapy import Spider
import logging

class PlaywrightLogsFilter(logging.Filter):
    def filter(self, record):
        return "[Context=default]" not in record.getMessage()

scrapy_logger = logging.getLogger("scrapy-playwright")
scrapy_logger.addFilter(PlaywrightLogsFilter())

media_extensions = [
    # Image formats
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", 
    ".svg", ".ico", ".avif", ".heif", ".heic", ".raw", ".cr2", ".nef", 
    ".orf", ".sr2", ".raf", ".arw", ".dng", ".rw2",

    # Video formats
    ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpg", 
    ".mpeg", ".3gp", ".ogv", ".mts", ".m2ts", ".ts",

    # css
    "css", "svg"
]

def should_abort_request(request):
    if request.resource_type in ["image", "video", "media", "stylesheet"]:
        return True
    if request.url.split('?')[0].split('.')[-1] in media_extensions:
        return True
    




class PlaywrightSpider(Spider):
    browsers = {
        "chrome":"chromium",
        "firefox":"firefox",
        "webkit":"webkit",
    }

    def __init_subclass__(cls, **kwargs):
        """Dynamically update settings to reflect subclass attributes."""
        cls.custom_settings = {
            "DOWNLOAD_HANDLERS": {
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "PLAYWRIGHT_LAUNCH_OPTIONS": {
                "headless": not getattr(cls, 'visible', False),
            },
            "PLAYWRIGHT_BROWSER_TYPE": cls.browsers[getattr(cls, 'browser', "chrome")],  # Uses subclass's `browser`
            "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": getattr(cls, 'timeout', 300) * 1000,
            "PLAYWRIGHT_MAX_CONTEXTS": getattr(cls, 'context', 4),
            "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": getattr(cls, 'pages', 5),
            "DOWNLOADER_MIDDLEWARES": {
                'core.playwright.middleware.PlaywrightMiddleware': 592,
            },
            "PLAYWRIGHT_ABORT_REQUEST":should_abort_request
        }
