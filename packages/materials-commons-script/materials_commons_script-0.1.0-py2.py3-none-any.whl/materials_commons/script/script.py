import os
import pathlib
import materials_commons.api as mcapi


def clean_path(path):
	if path.startswith("/"):
		path = path[1:]
	return path


def init():
	return Script()


class Script(object):
	def __init__(self):
		# Setup directory paths
		self.read_dir = pathlib.Path(os.getenv("READ_DIR"))
		self.write_dir = pathlib.Path(os.getenv("WRITE_DIR"))
		self.run_dir = pathlib.Path(os.getenv("RUN_DIR"))
		self.run_dir_in = self.read_dir / self.run_dir
		self.run_dir_out = self.write_dir / self.run_dir
		self.run_dir_out.mkdir(parents=True, exist_ok=True)

		# Setup mcapi related items
		self.c = mcapi.Client(os.getenv("MCAPIKEY"))
		self.project_id = os.getenv("PROJECT_ID")

	def open_project_file(self, path):
		return open(self.read_dir / clean_path(path), "r")

	def open_run_dir_file(self, path):
		return open(self.run_dir_in / clean_path(path), "r")

	def open_run_dir_out_file(self, path, mode):
		return open(self.run_dir_out / clean_path(path), mode)

	def open_project_out_file(self, path, mode):
		return open(self.write_dir / clean_path(path), mode)

	def mkdir_all(self, path):
		p = self.write_dir / clean_path(path)
		p.mkdir(parents=True, exist_ok=True)
