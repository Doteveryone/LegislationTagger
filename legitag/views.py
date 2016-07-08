from flask import request, render_template, send_from_directory, abort, redirect, url_for
from flask.ext.security import login_required, current_user
from legitag import app, models, forms
from mongoengine import DoesNotExist
import random
import requests


@app.route('/')
def index():
    legislations = models.Legislation.objects()
    return render_template('index.html', legislations=legislations, menu_item='tools')

@app.route('/about')
def about():
    return render_template('about.html', menu_item='about')

@app.route('/proxy')
def proxy():
    url = request.args.get('url', False)
    if url:
        if url.startswith('http://legislation.data.gov.uk') or url.startswith('http://legislation.gov.uk'):
            html =  requests.get(url).text
            html = html.replace('<link rel="stylesheet" href="/styles/HTML5_styles/secondary.css" type="text/css">', '')
            html = html.replace('<link rel="stylesheet" href="/styles/HTML5_styles/annotations.css" type="text/css">', '')
            html = html.replace('<link rel="stylesheet" href="/styles/HTML5_styles/prospective.css" type="text/css">', '')
            html = html.replace('<head>', '<head><link rel="stylesheet" href="/static/css/legislationgovuk.css" type="text/css">')

            return html
        else:
            abort(404)
    else:
        abort(404)


@app.route('/legislation/<id>', methods=['GET', 'POST'])
def legislation(id):
    try:
        legislation = models.Legislation.objects.get(id=id)
    except (DoesNotExist):
        abort(404)

    random = (request.args.get('random', False) == 'true')

    form = forms.TagForm()

    if request.method == 'POST':

        if not current_user.is_authenticated:
            abort(401)

        if form.validate():
            form = forms.TagForm(request.form)

            # policy areas
            for item in form.policy_area_tags.data.split(','):
                tag = models.Tag()
                tag.key = 'policy'
                tag.value = item.strip()
                legislation.append_tag(tag)

            # users
            for item in form.policy_area_tags.data.split(','):
                tag = models.Tag()
                tag.key = 'user'
                tag.value = item.strip()
                legislation.append_tag(tag)

            legislation.save(current_user, "Added tags")

            # if random, then off to another page
            if random:
                return redirect(url_for('random_legislation'))

    return render_template('legislation.html', legislation=legislation, form=form, random=random, menu_item='tools')

@app.route('/random')
def random_legislation():
    total = models.Legislation.objects.count()
    random_record = random.randint(0, total-1)
    legislation = models.Legislation.objects[random_record:].first()
    return redirect("%s?random=true" % url_for('legislation', id=legislation.id))

@app.route('/tags')
def tags():
    return render_template('tags.html', menu_item='tags')

