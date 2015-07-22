from dash import app
from flask import Flask, Response, render_template, request, flash, session, redirect, url_for
import subprocess, os, signal
from settings import *
from twitter import *


@app.route('/about')
def about(): 
  return render_template('about.html')

@app.route('/twitter/')
@app.route('/twitter/', methods=['POST'])
def twitter():
   if request.method == 'POST':
	search = request.form["search"]
	type = request.form["selectType"]

	if(type.lower() == "user"):
		time = Timeline(search)
		return render_template('twitter.html', tw=APP_TWITTER.search_tweets_iterable(time))
	elif(type.lower() == "all"):
		sr = Search()
		sr.set_keywords(search.split())
		sr.set_language('en')
		sr.set_include_entities(False)
		return render_template('twitter.html', tw=APP_TWITTER.search_tweets_iterable(sr))
   return render_template('twitter.html', tw=None)

@app.route('/')
def home():
  return render_template('home.html')

