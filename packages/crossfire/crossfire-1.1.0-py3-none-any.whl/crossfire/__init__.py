__version__ = "0.1.0"
__all__ = ("AsyncClient", "Client", "cities", "occurrences", "states")

from functools import lru_cache

from crossfire.clients import AsyncClient, Client  # noqa


@lru_cache(maxsize=1)
def client():
    return Client()


def states(format=None):
    return client().states(format=format)


def cities(city_id=None, city_name=None, state_id=None, format=None):
    return client().cities(
        city_id=city_id, city_name=city_name, state_id=state_id, format=format
    )


def occurrences(
    id_state,
    id_cities=None,
    type_occurrence="all",
    initial_date=None,
    final_date=None,
    max_parallel_requests=None,
    format=None,
    flat=False,
):
    return client().occurrences(
        id_state,
        id_cities=id_cities,
        type_occurrence=type_occurrence,
        initial_date=initial_date,
        final_date=final_date,
        max_parallel_requests=max_parallel_requests,
        format=format,
        flat=flat,
    )
