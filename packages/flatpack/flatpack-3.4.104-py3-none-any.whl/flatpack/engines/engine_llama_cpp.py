import os
import re
import socket
import subprocess
import tempfile


class LlamaCPPEngine:
    def __init__(self, model_path, llama_cpp_dir="llama.cpp", n_ctx=4096, n_threads=8, verbose=False):
        self.model_path = model_path
        self.llama_cpp_dir = llama_cpp_dir
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.verbose = verbose
        self.server_process = None
        self.setup_llama_cpp()
        self.start_server()

    def setup_llama_cpp(self):
        if not os.path.exists(self.llama_cpp_dir):
            try:
                print(f"📥 Cloning llama.cpp repository...")
                clone_result = subprocess.run(
                    ["git", "clone", "https://github.com/ggerganov/llama.cpp", self.llama_cpp_dir]
                )
                if clone_result.returncode != 0:
                    print(
                        "❌ Failed to clone the llama.cpp repository. Please check your internet connection and try again.")
                    return
                print(f"📥 Finished cloning llama.cpp repository into '{self.llama_cpp_dir}'")
            except Exception as e:
                print(f"❌ Failed to clone the llama.cpp repository. Error: {e}")
                return

        main_executable = os.path.join(self.llama_cpp_dir, "main")
        if not os.path.exists(main_executable):
            makefile_path = os.path.join(self.llama_cpp_dir, "Makefile")
            if os.path.exists(makefile_path):
                try:
                    print(f"🔨 Running 'make' in the llama.cpp directory...")
                    make_result = subprocess.run(["make"], cwd=self.llama_cpp_dir)
                    if make_result.returncode != 0:
                        print(
                            f"❌ Failed to run 'make' in the llama.cpp directory. Please check the logs for more details.")
                        return
                    print(f"🔨 Finished running 'make' in the llama.cpp directory")
                except Exception as e:
                    print(f"❌ Failed to run 'make' in the llama.cpp directory. Error: {e}")
                    return
            else:
                print(
                    f"❌ Makefile not found in the llama.cpp directory. Please ensure the repository is cloned correctly.")

    def start_server(self):
        command = (
            f"{os.path.join(self.llama_cpp_dir, 'main')} -m {self.model_path} -n {self.n_ctx} "
            f"-ngl 0 --ctx-size {self.n_ctx} --temp 1.0 --repeat-penalty 1.0 --server"
        )
        self.server_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if self.verbose:
            print(f"Started llama.cpp server with command: {command}")

    def generate_response(self, prompt, max_tokens):
        # Connect to the server and send the prompt
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 8080))  # Adjust the host and port as needed
            s.sendall(prompt.encode('utf-8'))
            s.sendall(b'\n')

            # Receive the response from the server
            response = s.recv(4096).decode('utf-8')

        return response

    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
