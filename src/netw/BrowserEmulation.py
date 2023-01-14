from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# TODO: Add support for at least Chrome, Chromium and Safari.
SUPPORTED_BROWSERS = ["Firefox"]


class BrowserEmulation:
    def __init__(self, withBrowser: str, onFile: str, runHeadless: bool = True):
        """
        This class is used to emulate a Web Browser, with the purpose of opening a file in the browser but
        not displaying anything to the user. This is because PeerJS uses WebRTC and WebRTC requires a HTML
        file to be opened in a browser.
        :param withBrowser: The name of the browser to emulate. Currently only Firefox is supported.
        :param onFile: This is the HTML file to open in the browser.
        :param runHeadless: This option defines if we display or not the browser.
        """
        if withBrowser.capitalize() not in SUPPORTED_BROWSERS:
            raise ValueError(f"The Web Broser {withBrowser} is not supported.")
        else:
            self.withBrowser = withBrowser.capitalize()
            self.runHeadless = runHeadless
            self.onFile = onFile
            self.webDriver = None

    def createOptions(self) -> "Options/None":
        options = None
        if self.withBrowser == "Firefox":
            options = webdriver.FirefoxOptions()
            if self.runHeadless:
                options.add_argument("--headless")

        return options

    def startDriver(self):
        if self.withBrowser == "Firefox":
            self.service = FirefoxService(GeckoDriverManager().install())
            self.webDriver = webdriver.Firefox(
                service=self.service, options=self.createOptions()
            )
            self.webDriver.get(self.onFile)

    def stopDriver(self):
        self.webDriver.quit()
        self.service.stop()

    def __str__(self):
        return f"BrowserEmulation: {self.withBrowser}"

    def __repr__(self):
        return f"BrowserEmulation: {self.withBrowser}"
