import os
import sys
import time

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from api.models import News
from integrations.gnews import GnewsAPI

news = GnewsAPI()


def fetch_news_category() -> None:
    """
    Busca noticia na API Gnews por categoria e salva no banco de dados
    """
    categories = news.categories
    categories_en = news.categories_en
    try:
        for category in categories:
            gnews_data = news.get_top_headlines(
                category=category,
                country="br",
                lang="pt",
                max_results=10,
            )
            if not gnews_data:
                print(f"Nenhuma noticia encontrada para a categoria{category}")

            news_processed = news.processes_data(
                gnews_data=gnews_data, category=categories_en[category]
            )

            try:
                for new in news_processed:

                    News.objects.create(
                        title=new["title"],
                        description=new["description"],
                        content=new["content"],
                        url=new["url"],
                        image_url=new["image_url"],
                        published_at=new["published_at"],
                        category=new["category"],
                        source=new["source"],
                    )

                time.sleep(2)

            except Exception as err:
                print(f"Erro ao salva noticia {new['title']}: {err}")

    except Exception as err:
        print(f"Erro ao processa categories {category}: {err} ")


def fetch_news() -> None:
    """
    Busca Noticia gerais e salva no banco
    """

    try:
        gnews_data = news.get_news(
            query="Brasil", country="br", lang="pt", max_results=10
        )

        if gnews_data:
            news_processed = news.processes_data(
                gnews_data=gnews_data, category="geral"
            )

            try:
                for new in news_processed:
                    News.objects.create(
                        title=new["title"],
                        description=new["description"],
                        content=new["content"],
                        url=new["url"],
                        image_url=new.get("image_url"),
                        published_at=new["published_at"],
                        category=new["category"],
                        source=new["source"],
                    )

            except Exception as err:
                print(f"Erro ao salva noticia {new['title']} : {err}")
        else:
            print("Erro ao busca noticias")

    except Exception as err:
        print(f"Erro ao busca noticias:{err}")


if __name__ == "__main__":
    fetch_news_category()
