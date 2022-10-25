# PRG1：ライブラリ設定
import fitz
import os

def extract_img(filename):
    # PRG3：PDFファイルを読み込む
    doc = fitz.open(filename)
    output_path=os.path.splitext(os.path.basename(filename))[0]
    output_dir=f"./AA/{output_path}"
    os.makedirs(output_dir, exist_ok=True)
    # PRG4：画像情報を格納するリストを作成
    images = []

    # PRG5：１ページずつ画像データを取得
    for page in range(len(doc)):
        images.append(doc[page].get_images())

    # PRG6：ページ内の画像情報を順番に処理
    for pageNo, image in enumerate(images):
        # PRG7：ページ内の画像情報を処理する
        if image != []:
            for i in range(len(image)):
                print(image[i])
                #continue
                # PRG8：画像情報の取得
                xref = image[i][0]
                # PRG9：マスク情報の取得と画像の再構築
                pix = fitz.Pixmap(doc.extract_image(xref)["image"])
                pic=doc.extract_image(xref)
                print(pic)
                ext=pic["ext"]
                # PRG10：画像を保存
                img_name = os.path.join(output_dir, f'image{pageNo+1}_{i}.{ext}')
                with open(img_name, "wb") as f:
                    f.write(pic["image"])
    doc.close()

import glob
files = glob.glob("./pdf/*.pdf")
for file in files:
    extract_img(file)