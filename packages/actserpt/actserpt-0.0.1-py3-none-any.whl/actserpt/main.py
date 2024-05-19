def new_wizard_in_desktop(type, userprofile, documentname):
    if type == 'folder':
        import os
        desktop_path = os.path.join(os.path.join(os.environ[userprofile]), 'Desktop')
        folder_name = documentname
        new_folder_path = os.path.join(desktop_path, folder_name)
        os.makedirs(new_folder_path)
    if type == 'text':
        import os
        desktop_path = os.path.join(os.path.join(os.environ[userprofile]), 'Desktop')
        file_name = documentname+".txt"
        file_path = os.path.join(desktop_path, file_name)
        with open(file_path, 'w') as file:
            file.write("This text file made by 'actserpt'.")
    if type == 'html':
        import os
        kullanıcı_profil = os.environ.get(userprofile)
        dosya_adı = documentname+".html"
        dosya_yolu = os.path.join(kullanıcı_profil, "Desktop")
        html_icerik = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>actserpt</title>
        </head>
        <body>
            <h1>Description: </h1>
            <p>This HTML file is made by 'actserpt'.</p>
        </body>
        </html>
        """
        with open(os.path.join(dosya_yolu, dosya_adı), "w") as dosya:
            dosya.write(html_icerik)
    if type == 'java':
        import os
        kullanıcı_profil = os.environ.get(userprofile)
        dosya_adı = documentname+".java"
        dosya_yolu = os.path.join(kullanıcı_profil, "Desktop")
        java_icerik = """
        public class HelloWorld {
            public static void main(String[] args) {
                System.out.println("This Java document made by 'actserpt'.");
            }
        }
        """
        with open(os.path.join(dosya_yolu, dosya_adı), "w") as dosya:
            dosya.write(java_icerik)

def write_python(command):
    eval(command)

def valuename(documentname):
    print(type(documentname))