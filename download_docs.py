import os
import requests
import base64

def download_github_folder(repo_owner, repo_name, path, local_path):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        contents = response.json()
        
        for item in contents:
            if item['type'] == 'file':
                file_path = os.path.join(local_path, item['name'])
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                file_url = item['download_url']
                file_content = requests.get(file_url).content
                
                with open(file_path, 'wb') as file:
                    file.write(file_content)
                print(f"Downloaded: {file_path}")
            
            elif item['type'] == 'dir':
                new_path = os.path.join(path, item['name'])
                new_local_path = os.path.join(local_path, item['name'])
                download_github_folder(repo_owner, repo_name, new_path, new_local_path)

if __name__ == "__main__":
    repo_owner = "gptscript-ai"
    repo_name = "gptscript"
    github_path = "docs/docs"
    local_path = "gptscript-docs"
    
    download_github_folder(repo_owner, repo_name, github_path, local_path)
    print("Download completed!")
