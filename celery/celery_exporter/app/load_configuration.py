import yaml
import os

def load_configuration():
  config_file = 'configuration.yml'
  file_path = os.path.abspath(os.path.dirname('__file__'))

  config = os.path.join(file_path + '/app', config_file)
  with open(config, 'r') as f:
    configuration = yaml.load(f, Loader=yaml.FullLoader)
  f.close()
  return configuration

def get_urls():
  config = load_configuration()
  return config['urls']
                        
