"""Playwright Browser Controller für autonome Browser-Automatisierung."""

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from typing import Optional, Dict, List
from loguru import logger
import asyncio


class BrowserController:
    """Controller für Browser-Automatisierung mit Playwright.
    
    Ermöglicht autonome Steuerung eines Browsers für
    Recherche, Interaktion und Datenextraktion.
    """
    
    def __init__(
        self,
        headless: bool = False,
        viewport: Dict = None,
        user_agent: Optional[str] = None
    ):
        """Initialisiert den Browser Controller.
        
        Args:
            headless: Browser im Headless-Modus starten
            viewport: Viewport-Größe {"width": 1920, "height": 1080}
            user_agent: Custom User-Agent String
        """
        self.headless = headless
        self.viewport = viewport or {"width": 1920, "height": 1080}
        self.user_agent = user_agent
        
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        logger.info(f"Browser Controller initialisiert (headless={headless})")
    
    async def start(self):
        """Startet den Browser."""
        try:
            self.playwright = await async_playwright().start()
            
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            context_options = {
                "viewport": self.viewport,
                "ignore_https_errors": True
            }
            if self.user_agent:
                context_options["user_agent"] = self.user_agent
            
            self.context = await self.browser.new_context(**context_options)
            self.page = await self.context.new_page()
            
            logger.info("Browser erfolgreich gestartet")
            
        except Exception as e:
            logger.error(f"Fehler beim Start des Browsers: {e}")
            raise
    
    async def navigate(self, url: str, wait_until: str = "networkidle"):
        """Navigiert zu einer URL.
        
        Args:
            url: Ziel-URL
            wait_until: Warte-Bedingung (load, domcontentloaded, networkidle)
        """
        try:
            await self.page.goto(url, wait_until=wait_until)
            logger.info(f"Navigiert zu: {url}")
        except Exception as e:
            logger.error(f"Navigationsfehler: {e}")
            raise
    
    async def click(self, selector: str, timeout: int = 30000):
        """Klickt auf ein Element.
        
        Args:
            selector: CSS/XPath Selektor
            timeout: Timeout in Millisekunden
        """
        try:
            await self.page.click(selector, timeout=timeout)
            logger.debug(f"Klick auf: {selector}")
        except Exception as e:
            logger.error(f"Klick-Fehler auf {selector}: {e}")
            raise
    
    async def fill(self, selector: str, text: str):
        """Füllt ein Eingabefeld.
        
        Args:
            selector: CSS/XPath Selektor
            text: Einzugebender Text
        """
        try:
            await self.page.fill(selector, text)
            logger.debug(f"Text eingegeben in: {selector}")
        except Exception as e:
            logger.error(f"Eingabefehler bei {selector}: {e}")
            raise
    
    async def get_text(self, selector: str) -> str:
        """Extrahiert Text von einem Element.
        
        Args:
            selector: CSS/XPath Selektor
            
        Returns:
            Der extrahierte Text
        """
        try:
            element = await self.page.query_selector(selector)
            if element:
                text = await element.inner_text()
                return text
            return ""
        except Exception as e:
            logger.error(f"Text-Extraktion fehlgeschlagen: {e}")
            return ""
    
    async def screenshot(self, path: str, full_page: bool = False):
        """Erstellt einen Screenshot.
        
        Args:
            path: Speicherpfad
            full_page: Gesamte Seite oder nur Viewport
        """
        try:
            await self.page.screenshot(path=path, full_page=full_page)
            logger.info(f"Screenshot gespeichert: {path}")
        except Exception as e:
            logger.error(f"Screenshot-Fehler: {e}")
            raise
    
    async def evaluate(self, script: str):
        """Führt JavaScript aus.
        
        Args:
            script: JavaScript Code
            
        Returns:
            Rückgabewert des Scripts
        """
        try:
            result = await self.page.evaluate(script)
            return result
        except Exception as e:
            logger.error(f"JavaScript-Fehler: {e}")
            raise
    
    async def wait_for_selector(self, selector: str, timeout: int = 30000):
        """Wartet auf ein Element.
        
        Args:
            selector: CSS/XPath Selektor
            timeout: Timeout in Millisekunden
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
        except Exception as e:
            logger.error(f"Warte-Timeout für {selector}: {e}")
            raise
    
    async def get_page_content(self) -> str:
        """Gibt den vollständigen HTML-Inhalt zurück.
        
        Returns:
            HTML Content der Seite
        """
        try:
            content = await self.page.content()
            return content
        except Exception as e:
            logger.error(f"Content-Fehler: {e}")
            return ""
    
    async def close(self):
        """Schließt den Browser."""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            
            logger.info("Browser geschlossen")
            
        except Exception as e:
            logger.error(f"Fehler beim Schließen: {e}")
