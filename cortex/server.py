#!/usr/bin/python
from pathlib import Path as path
import struct
from datetime import datetime
import threading
from flask import Flask
from flask import request
import pika
import click

class Log:
    
    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info(): # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()

@click.group()
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


@main.command('run-server')
@click.option('-h','--host', default='127.0.0.1')
@click.option('-p','--port', default=8000)
@click.argument('publish', default='rabbitmq://127.0.0.1:5672/')
def run_server(host, port, publish):
    publish = publish
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='snapshots',exchange_type='fanout')
    #channel.queue_declare(queue='current_snapshots')
    app = Flask(__name__)

    @app.route('/config', methods = ['GET'])
    def myParsers():
        print("in server parsers")
        return "hello parsers"

    @app.route('/snapshot', methods = ['POST'])
    def newSnapshot():
        print("in server snapshot")
        snapshot = request.get_data()
        channel.basic_publish(exchange='snapshots',
                              routing_key='',
                              body=snapshot)
        print("done")
        return "ok"
        #publish(snapshot)

    app.run(host = host,port = port,threaded=True)


if __name__ == '__main__':
    main()
