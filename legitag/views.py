from flask import request, render_template, send_from_directory, abort, redirect, url_for
from flask.ext.security import login_required, current_user
from legitag import app, models, forms
from mongoengine import DoesNotExist
import random


@app.route('/')
def index():
    legislations = models.Legislation.objects()
    return render_template('index.html', legislations=legislations, menu_item='tools')

@app.route('/about')
def about():
    return render_template('about.html', menu_item='about')


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

