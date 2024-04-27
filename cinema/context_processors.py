from .forms import MoviesSearchForm


def movies_search_form(request):
    return {'search_form': MoviesSearchForm()}
