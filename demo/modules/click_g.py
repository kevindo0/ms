import click

# option参数：
# hide_input: boole 为True，就能隐藏
# default： 设置命令行参数的默认值
# required：是否为必填参数
# prompt： 当在命令行中没有输入相应的参数时，会更具prompt提示用户输入
# type：参数类型，可以是string、int、float等

@click.command()
@click.option('-c',required=True,type=click.Choice(['start','stop']))
@click.option('--pwd', default='123456', prompt='you password', hide_input=True)
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
@click.option('--start', type=click.DateTime())
def hello(c, pwd, count, name, start):
    print("c:", c)
    print("pwd:", pwd)
    print('start:', start)
    for x in range(count):
        click.echo('Hello %s!' % name)

# group cli
# chain: bool 为True时多个子命令顺序执行，否则只能执行一个子命令
@click.group(chain=True)
def cli():
    pass

@cli.command("t1")
def initdb():
    click.echo('Initialized the database')
    
@cli.command("t2")
def dropdb():
    click.echo('Dropped the database')

# nargs : 表接收几个参数
# python click_g.py a.txt b.txt c.txt d.txt e.txt
# src; ('a.txt', 'b.txt')
# dst: c.txt
# three: ('d.txt', 'e.txt')
@click.command()
@click.argument('src', nargs=-1)
@click.argument('dst', nargs=1)
@click.argument('three', nargs=2)
def copy(src, dst, three):
    """Move file SRC to DST."""
    print('src;', src)
    print('dst:', dst)
    print('three:', three)

if __name__ == '__main__':
    hello()
    # cli()
    # copy()

