from flask import request, render_template, send_from_directory, abort, redirect, url_for, flash
from flask.ext.security import login_required, current_user
from legitag import app, models, forms
from mongoengine import DoesNotExist
import random
import requests

@app.route('/')
def index():
    edit_count = models.EditCount.objects.order_by('-count')
    return render_template('index.html', edit_count=edit_count, menu_item='tools')

@app.route('/about')
def about():
    return render_template('about.html', menu_item='about')

@app.route('/proxy')
def proxy():
    try:
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
    except:
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
                if item.strip() != '':
                    tag = models.Tag()
                    tag.key = 'policy'
                    tag.value = item.strip().lower()
                    legislation.append_tag(tag)

            # users
            for item in form.users_affected_tags.data.split(','):
                if item.strip() != '':
                    tag = models.Tag()
                    tag.key = 'user'
                    tag.value = item.strip().lower()
                    legislation.append_tag(tag)

            #organisations
            for item in form.organisation_tags.data.split(','):
                if item.strip() != '':
                    tag = models.Tag()
                    tag.key = 'organisation'
                    tag.value = item.strip().lower()
                    legislation.append_tag(tag)

            #custom
            for item in form.advanced_tags.data:
                key = item['key'].strip().lower()
                value = item['value'].strip().lower()
                if key != ''and value != '':
                    tag = models.Tag()
                    tag.key = key
                    tag.value = value
                    legislation.append_tag(tag)

            try:
                legislation.save(current_user, "Added tags")
                # if random, then off to another page
                if random:
                    flash('Thanks, your tags have been added. <a href="%s">Click here to go back to it</a>.' % url_for('legislation', id=legislation.id))
                    return redirect(url_for('random_legislation'))
                else:
                    flash('Thanks, your tags have been added.')
            except:
                flash('Sorry, something went wrong.')


    return render_template('legislation.html', legislation=legislation, form=form, random=random, menu_item='tools')

@app.route('/random')
def random_legislation():
    total = models.Legislation.objects.count()
    random_record = random.randint(0, total-1)
    legislation = models.Legislation.objects[random_record:].first()
    return redirect("%s?random=true" % url_for('legislation', id=legislation.id))

@app.route('/tags')
def tags():
    tags = models.Legislation.objects.distinct('_tags')
    tags.sort(key=lambda x: x.key)

    return render_template('tags.html', menu_item='tags', tags=tags)

@app.route('/tags/<tag>')
def tag_browse(tag):
    tag_split = tag.split(':')
    legislations = models.Legislation.objects(_tags__key=tag_split[0], _tags__value=tag_split[1])
    return render_template('tags_browse.html', menu_item='tags', tag=tag, legislations=legislations)

@app.route('/search')
def search():
    query = request.args.get('q', False)
    legislations = []
    if query:
        legislations = models.Legislation.objects.search_text(query).order_by('$text_score')
    return render_template('search.html', menu_item='search', legislations=legislations, query=query)