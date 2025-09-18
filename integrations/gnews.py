
import requests
from decouple import config



class GnewsAPI:
    """
    Classe pra Intregacao com a api da Gnews
    """

    def __init__(self):
        self._api_key = config("API_KEY_GNEWS")
        self.base_url = f"https://gnews.io/api/v4/"
        self.session = requests.Session()
        self.categories = ["general", "sports", "technology", "business"]
        self.categories_en = {
            "general": "geral",
            "sports": "esportes",
            "technology": "tecnologia",
            "business": "negócios",
        }

    def get_news(self, query: str, country: str, lang: str, max_results: int) -> list:
        """
        Busca noticia no Brasil retorna dados
        """

        params = {
            "q": query,
            "country": country,
            "lang": lang,
            "max_results": max_results,
            "apikey": self._api_key,
        }
        url = f"{self.base_url}search"

        try:
            response = self.session.get(url, params=params)

            if response.ok:
                news = response.json()

                if "articles" in news:
                    articles = news["articles"]

                    return articles

                else:
                    return "articles nao retorna da api"

            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise RuntimeError(f"Erro ao buscar notícias: {err}")

    def get_top_headlines(
        self, category: str, country: str, lang: str, max_results: int
    ) -> list:
        """
        Busca noticia por categoria
        """

        params = {
            "category": category,
            "country": country,
            "lang": lang,
            "max_results": max_results,
            "apikey": self._api_key,
        }
        url = f"{self.base_url}top-headlines?"

        try:
            response = self.session.get(url, params=params)

            if response.ok:
                news = response.json()

                if "articles" in news:
                    articles = news["articles"]
                    return articles

                else:
                    return "articles nao retorna da api"

            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise RuntimeError(f"Erro ao buscar notícias: {err}")

    def processes_data(self, gnews_data: list, category: str) -> list:
        """
        Processa os dados buscado na api e formata pro ser inserido no banco
        """

        news_processed = []

        for new in gnews_data:
            news_processed.append(
                {
                    "title": new["title"],
                    "description": new["description"],
                    "content": new["content"],
                    "url": new["url"],
                    "image_url": new["image"],
                    "published_at": new["publishedAt"],
                    "category": category,
                    "source": new["source"]["name"],
                }
            )
        return news_processed
