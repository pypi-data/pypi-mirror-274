from llama_cpp import Llama


class LlamaCPPEngine:
    def __init__(self, repo_id=None, filename=None, n_ctx=4096, n_threads=8, verbose=False):
        if repo_id:
            self.model = Llama.from_pretrained(
                echo=False,
                filename=filename,
                n_ctx=n_ctx,
                n_threads=n_threads,
                repeat_penalty=1.0,
                repo_id=repo_id,
                seed=-1,
                streaming=True,
                temp=1.0,
                verbose=verbose
            )
        else:
            self.model = Llama(
                echo=False,
                model_path=filename,
                n_ctx=n_ctx,
                n_threads=n_threads,
                repeat_penalty=1.0,
                seed=-1,
                streaming=True,
                temp=1.0,
                verbose=verbose
            )

    def generate_response(self, context, question, max_tokens):
        prompt = f"""
        Context: {context}\n
        Question: {question}\n
        """
        # Stream the output
        response_chunks = self.model.stream(
            f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
            max_tokens=max_tokens,
            stop=["<|end|>"],
            echo=False
        )

        response_text = ""
        for chunk in response_chunks:
            if 'choices' in chunk and chunk['choices']:
                response_text += chunk['choices'][0]['text']

        return response_text
