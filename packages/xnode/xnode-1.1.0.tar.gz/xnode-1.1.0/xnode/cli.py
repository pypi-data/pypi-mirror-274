import os
import sys
import time
import platform
import posixpath
import re
import threading
import serial.serialutil
from genlib.ansiec import ANSIEC
import click
import dotenv

config = dotenv.find_dotenv(filename=".xnode", usecwd=True)
if config:
    dotenv.load_dotenv(dotenv_path=config)

import xnode.files as files
import xnode.pyboard as pyboard

_board = None

def windows_full_port_name(portname):
    m = re.match("^COM(\d+)$", portname)
    if m and int(m.group(1)) < 10:
        return portname
    else:
        return "\\\\.\\{0}".format(portname)

@click.group()
@click.option(
    "--sport",
    "-s",
    envvar="SERIAL_PORT",
    required=True,
    type=click.STRING,
    help="Name of serial port for connected board.",
    metavar="SPORT",
)
@click.option(
    "--baud",
    '-b',
    envvar="SERIAL_BAUD",
    default=115200,
    type=click.INT,
    help="Baud rate for the serial connection (default 115200).",
    metavar="BAUD",
)
def cli(sport, baud):
    global _board

    if platform.system() == "Windows":
        sport = windows_full_port_name(sport)

    _board = pyboard.Pyboard(sport, baud)

@cli.command()
@click.argument("remote_file")
@click.argument("local_file", type=click.File("wb"), required=False)
def get(remote_file, local_file):
    board_files = files.Files(_board)
    contents = board_files.get(remote_file)

    if local_file is None:
        print(contents.decode("utf-8"))
    else:
        local_file.write(contents)

@cli.command()
@click.option(
    "--exists-okay", is_flag=True, help="Ignore if the directory already exists."
)
@click.argument("directory")
def mkdir(directory, exists_okay):
    board_files = files.Files(_board)
    board_files.mkdir(directory, exists_okay=exists_okay)

@cli.command()
@click.argument("directory", default="/")
def ls(directory):
    board_files = files.Files(_board)
    for f in board_files.ls(directory):
        print(f)

def __dir_put(local, remote):
    board_files = files.Files(_board)
    for parent, child_dirs, child_files in os.walk(local, followlinks=True):
        remote_parent = posixpath.normpath(
            posixpath.join(remote, os.path.relpath(parent, local))
        )
        try:
            board_files.mkdir(remote_parent)
        except files.DirectoryExistsError:
            pass
        for filename in child_files:
            with open(os.path.join(parent, filename), "rb") as infile:
                remote_filename = posixpath.join(remote_parent, filename)
                board_files.put(remote_filename, infile.read())

@cli.command()
@click.argument("local", type=click.Path(exists=True))
@click.argument("remote", required=False)
def put(local, remote):
    if remote is None:
        remote = os.path.basename(os.path.abspath(local))
    if os.path.isdir(local):
        __dir_put(local, remote)
    else:
        with open(local, "rb") as infile:
            board_files = files.Files(_board)
            board_files.put(remote, infile.read())
    
@cli.command()
@click.argument("remote_file")
def rm(remote_file):
    board_files = files.Files(_board)
    board_files.rm(remote_file)

@cli.command()
@click.option(
    "--missing-okay", is_flag=True, help="Ignore if the directory does not exist."
)
@click.argument("remote_folder")
def rmdir(remote_folder, missing_okay):
    board_files = files.Files(_board)
    board_files.rmdir(remote_folder, missing_okay=missing_okay)

@cli.command()
@click.argument("type")
def format(type):
    board_files = files.Files(_board)
    if type.lower() == 'a':
        board_files.format_a()
    elif type.lower() == 'b':
        board_files.format_b()
    else:
        print("failed type")

@cli.command()
@click.argument("local_file")
@click.option(
    "--no-stream",
    "-n",
    is_flag=True,
    help="Do not join input/output stream",
)
@click.option(
    "--input-on",
    "-i",
    is_flag=True,
    help="Turn on echo for input",
)
def run(local_file, no_stream, input_on):
    board_files = files.Files(_board)
    try:
        board_files.run(local_file, not no_stream, input_on)
    except IOError:
        click.echo(
            "Failed to find or read input file: {0}".format(local_file), err=True
        )

@cli.command()
@click.option(
    "--hard",
    "mode",
    flag_value="NORMAL",
    help="Perform a hard reboot, including running init.py",
)
def reset(mode):
    _board.enter_raw_repl()
    if mode == "SOFT":
        _board.exit_raw_repl()
        return

    _board.exec_(
    """if 1:
        def reset():
            import machine
            machine.reset()
        """
    )

    try:
         _board.exec_raw_no_follow("reset()")
    except serial.serialutil.SerialException as e:
        pass


serial_reader_running = None
serial_out_put_enable = True
serial_out_put_count = 0

def repl_serial_to_stdout(serial):
    global serial_out_put_count

    def hexsend(string_data=''):
        hex_data = string_data.decode("hex")
        return hex_data

    try:
        data = b''
        while serial_reader_running:
            count = serial.inWaiting()

            if count == 0:
                time.sleep(0.01)
                continue

            if count > 0:
                try:
                    data += serial.read(count)

                    if len(data) < 20:
                        try:
                            data.decode()
                        except UnicodeDecodeError:
                            continue

                    if data != b'':
                        if serial_out_put_enable and serial_out_put_count > 0:
                            if platform.system() == 'Windows':   
                                sys.stdout.buffer.write(data.replace(b"\r", b""))
                            else:
                                sys.stdout.buffer.write(data)
                                
                            sys.stdout.buffer.flush()
                    else:
                        serial.write(hexsend(data))

                    data = b''
                    serial_out_put_count += 1

                except:
                    return
    except KeyboardInterrupt:
        if serial != None:
            serial.close()

@cli.command()
def repl():
    global serial_reader_running
    global serial_out_put_enable
    global serial_out_put_count

    serial_out_put_count = 1

    serial_reader_running = True

    _board.read_until(1, b'\x3E\x3E\x3E', timeout=1)

    serial = _board.serial

    repl_thread = threading.Thread(target=repl_serial_to_stdout, args=(serial,), name='REPL')
    repl_thread.daemon = True
    repl_thread.start()

    if platform.system() == 'Windows':   
        import msvcrt as getch
    else:
        import getch
        
    serial.write(b'\r')

    count = 0

    while True:
        char = getch.getch()
    
        if char == b'\x16':
            char = b'\x03'

        count += 1
        if count == 1000:
            time.sleep(0.1)
            count = 0

        if char == b'\x07':
            serial_out_put_enable = False
            continue

        if char == b'\x0F':
            serial_out_put_enable = True
            serial_out_put_count = 0
            continue

        if char == b'\x00' or not char:
            continue

        if char == b'\x18':   # Ctrl + x to exit repl mode
            serial_reader_running = False
            serial.write(b' ')
            time.sleep(0.1)
            print('')
            break

        if char == b'\n':
            serial.write(b'\r')
        else:
            serial.write(char)

@cli.command()
def scan():
    pass

is_stoped = None

def show_waiting(delay):
    while not is_stoped:
        for ch in ('|', '/', '-', '\\', '|', '/', '-', '\\'):
            print(ANSIEC.OP.left() + ch, end='', flush=True)
            time.sleep(delay)
        
@cli.command()
def init():
    global is_stoped
    
    print("Fromat XNode")
    is_stoped = False
    threading.Thread(target=show_waiting, args=(20/1000,), daemon=True).start()
    board_files = files.Files(_board)
    board_files.format_b()
    is_stoped = True
    
    print(ANSIEC.OP.left() + "Install pop library on XNode")
    
    board_files.mkdir("/flash/lib/xnode", False)
    is_stoped = False
    threading.Thread(target=show_waiting, args=(20/1000,), daemon=True).start()        
    local = os.path.join(os.path.dirname(__file__), "pop")
    remote =  "/flash/lib/xnode/pop"
    __dir_put(local, remote)
    board_files.rmdir("/flash/lib/xnode/pop/__pycache__", False)

    is_stoped = True
    
    print(ANSIEC.OP.left() + "The job is done!")          