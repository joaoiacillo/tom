#!/usr/bin/env python3

import os
import subprocess

PROJECTS_DIR = os.environ.get('TOM_HOME', '.') + '/projects'

os.makedirs(PROJECTS_DIR, exist_ok=True)


def quick_fwrite(filename, content):
  with open(filename, 'w') as f:
    f.write(content)


def is_port_in_use(port):
  """
  Checks if the given port is already in use by any project.

  Args:
      port: The port to check.
  Returns:
      True if the port is in use, False otherwise.
  """
  import yaml

  projects = [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]
  for project in projects:
    docker_compose_path = os.path.join(PROJECTS_DIR, project, 'docker-compose.yml')
    if os.path.exists(docker_compose_path):
      with open(docker_compose_path, 'r') as f:
        compose_content = yaml.safe_load(f)
        services = compose_content.get('services', {})
        for service in services.values():
          service_ports = service.get('ports', [])
          for service_port in service_ports:
            host_port = service_port.split(':')[0]
            if host_port == port:
              return True
  return False


def command_new(args, rest):
  """
  Creates a new project with the given name and optional port.

  Args:
      args: Namespace object containing parsed arguments.
      rest: List of remaining arguments.
  """
  project_name = rest[0]
  project_path = os.path.join(PROJECTS_DIR, project_name)

  if os.path.exists(project_path):
    print(f'project \'{project_name}\' already exists')
    return

  host_port = args.port.split(':')[0]
  port_in_use = '\n      # warning: host port %s was already used, it might cause conflict.' % (host_port,) if is_port_in_use(host_port) else ''

  os.makedirs(project_path)
  os.chdir(project_path)

  quick_fwrite('.dockerignore', '.git/\n')
  quick_fwrite('docker-compose.yml', f"""services:
  app:
    image: {args.image}
    ports:{port_in_use}
      - '{args.port}'

networks:
  app-default:
""")
  
  if args.editor != 'none':
    subprocess.run([args.editor, 'docker-compose.yml'])

  if not args.no_git:
    subprocess.run(['git', 'init', '-q'])
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-q', '-m', 'init project'])

  os.chdir(os.path.dirname(project_path))
  print(f'project \'{project_name}\' created successfully')


def command_edit(args, rest):
  """
  Opens the docker-compose.yml file in the given editor.

  Args:
      args: Namespace object containing parsed arguments.
      rest: List of remaining arguments.
  """
  project_name = rest[0] if rest else None

  if project_name is not None:
    project_path = os.path.join(PROJECTS_DIR, project_name)
    os.chdir(project_path)
  else:
    project_path = os.getcwd()

  if args.editor == 'none':
    print('no editor specified')
    return

  if os.path.exists(os.path.join(project_path, 'docker-compose.yml')):
    subprocess.run([args.editor, 'docker-compose.yml'])
  else:
    print(f'unknown project or docker compose file not found')


def command_list(args, rest):
  """
  Lists all projects.

  Args:
      args: Namespace object containing parsed arguments.
      rest: List of remaining arguments.
  """
  rest = ['*'] if not rest else rest
  projects = [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]
  if projects:
    for project in projects:
      for r in rest:
        if r in project or r == '*':
          print(project)
  else:
    print('no projects available')


def command_remove(args, rest):
  """
  Deletes a project.

  Args:
      args: Namespace object containing parsed arguments.
      rest: List of remaining arguments.
  """
  project_name = rest[0]
  project_path = os.path.join(PROJECTS_DIR, project_name)

  if not args.force:
    confirmation = input(f'are you sure you want to delete project \'{project_name}\'? (y/n) ')
    if confirmation.lower() != 'y':
      return

  if os.path.exists(project_path):
    import shutil
    shutil.rmtree(project_path)
    print(f'project \'{project_name}\' deleted successfully')
  else:
    print(f'project \'{project_name}\' does not exist')


def command_up(args, rest):
  """
  Runs docker-compose up.

  Args:
      args: Namespace object containing parsed arguments.
      rest: List of remaining arguments.
  """
  project_name = rest[0] if rest and not rest[0].startswith('-') else None
  if project_name:
    project_path = os.path.join(PROJECTS_DIR, project_name)
    if os.path.exists(project_path):
      subprocess.run(['docker', 'compose', '-f', f'{project_path}/docker-compose.yml', 'up', *rest[1:]])
    else:
      print(f'project \'{project_name}\' does not exist')
  else:
    subprocess.run(['docker', 'compose', 'up', *rest])


def command_down(args, rest):
  """
  Runs docker-compose down.

  Args:
      args: Namespace object containing parsed arguments.
      rest: List of remaining arguments.
  """
  if args.all:
    containers = subprocess.run(['docker', 'ps', '-a', '-q'], stdout=subprocess.PIPE).stdout.decode().splitlines()
    subprocess.run(['docker', 'stop', *containers])
    return

  project_name = rest[0] if rest and not rest[0].startswith('-') else None
  if project_name:
    project_path = os.path.join(PROJECTS_DIR, project_name)
    if os.path.exists(project_path):
      subprocess.run(['docker', 'compose', '-f', f'{project_path}/docker-compose.yml', 'down', *rest[1:]])
    else:
      print(f'project \'{project_name}\' does not exist')
  else:
    subprocess.run(['docker', 'compose', 'down', *rest])


def command_ps(args, rest):
  """
  Runs docker-compose ps or docker ps.

  Args:
      args: Namespace object containing parsed arguments.
      rest: List of remaining arguments.
  """
  if args.docker:
    subprocess.run(['docker', 'ps', *rest])
    return

  project_name = rest[0] if rest and not rest[0].startswith('-') else None
  if project_name:
    project_path = os.path.join(PROJECTS_DIR, project_name)
    if os.path.exists(project_path):
      subprocess.run(['docker', 'compose', 'ps', '-f', f'{project_path}/docker-compose.yml', *rest[1:]])
    else:
      print(f'project \'{project_name}\' does not exist')
  else:
    if os.path.exists('docker-compose.yml'):
      subprocess.run(['docker', 'compose', 'ps', *rest])
      return
    subprocess.run(['docker', 'ps', *rest])


def command_ports(args, rest):
  """
  Lists all ports used by the projects, grouped by project.

  Args:
      args: Namespace object containing parsed arguments.
      rest: List of remaining arguments.
  """
  import yaml

  projects = [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]
  project_ports = {}

  for project in projects:
    docker_compose_path = os.path.join(PROJECTS_DIR, project, 'docker-compose.yml')
    if os.path.exists(docker_compose_path):
      with open(docker_compose_path, 'r') as f:
        compose_content = yaml.safe_load(f)
        services = compose_content.get('services', {})
        ports = []
        for service in services.values():
          service_ports = service.get('ports', [])
          ports.extend(service_ports)
        if ports:
          project_ports[project] = ports

  if project_ports:
    for project, ports in project_ports.items():
      print(f'{project}: {" ".join(ports)}')
  else:
    print('no ports found')


def create_argparser():
  from argparse import ArgumentParser

  parser = ArgumentParser(
    description='Common commands for daily project development with Docker'
  )

  parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

  commands = parser.add_subparsers(title='commands', dest='command')

  new_parser = commands.add_parser('new', help='create new projects')
  new_parser.add_argument('-p', '--port', help='main port mapping', type=str, default='8080:80')
  new_parser.add_argument('-i', '--image', help='base image', type=str, default='hello-world:latest')
  new_parser.add_argument('--no-git', help='stop git from initializing', action='store_false')
  new_parser.add_argument('--editor', help='editor to open the docker-compose.yml file', type=str, default='vim')
  new_parser.set_defaults(func=command_new)

  list_parser = commands.add_parser('ls', help='list projects')
  list_parser.set_defaults(func=command_list)

  path_parser = commands.add_parser('path', help='print project absolute path')
  path_parser.set_defaults(func=lambda args, rest: print(os.path.join(PROJECTS_DIR, rest[0])))

  ports_parser = commands.add_parser('ports', help='list all ports used by the projects')
  ports_parser.set_defaults(func=command_ports)

  edit_parser = commands.add_parser('edit', help='edit docker-compose.yml files')
  edit_parser.add_argument('--editor', help='editor to open the file', type=str, default='vim')
  edit_parser.set_defaults(func=command_edit)

  del_parser = commands.add_parser('rm', help='remove projects')
  del_parser.add_argument('-f', '--force', help='force delete', action='store_true')
  del_parser.set_defaults(func=command_remove)

  up_parser = commands.add_parser('up', help='start containers')
  up_parser.set_defaults(func=command_up)

  down_parser = commands.add_parser('down', help='stop containers')
  down_parser.add_argument('-a', '--all', help='stop all containers', action='store_true')
  down_parser.set_defaults(func=command_down)

  ps_parser = commands.add_parser('ps', help='list containers from a project or globally')
  ps_parser.add_argument('-d', '--docker', help='list global containers', action='store_true')
  ps_parser.set_defaults(func=command_ps)

  wash_parser = commands.add_parser('wash', help='prune stopped containers')
  wash_parser.set_defaults(func=lambda args, rest: subprocess.run(['docker', 'container', 'prune', '-f']))

  return parser


if __name__ == '__main__':
  argparser = create_argparser()
  args, rest = argparser.parse_known_args()

  if hasattr(args, 'func'):
    args.func(args, rest)
  
  if args.command is None:
    argparser.print_help()
