import struct


def to_csv(name, max_data):
    # 레이블 파일과 이미지 파일 열기
    lbl_f = open('./mnist/' + name + '-labels-idx1-ubyte', 'rb')
    img_f = open('./mnist/' + name + '-images-idx3-ubyte', 'rb')
    csv_f = open('./mnist/' + name + '.csv', 'w', encoding='utf-8')

    # 헤더 정보 읽기
    mag, lbl_count = struct.unpack('>II', lbl_f.read(8))
    mag, img_count = struct.unpack('>II', img_f.read(8))
    rows, cols = struct.unpack('>II', img_f.read(8))
    pixels = rows * cols

    # 이미지 데이터를 읽고 CSV 로 저장하기
    res = []
    for idx in range(lbl_count):
        if idx > max_data:
            break
        label = struct.unpack('B', lbl_f.read(1))[0]
        b_data = img_f.read(pixels)
        s_data = list(map(lambda n: str(n), b_data))
        csv_f.write(str(label) + ',')
        csv_f.write(','.join(s_data) + '\n')

        # 잘 저장됐는지 이미지 파일로 저장해서 테스트하기
        if idx < 10:
            s = 'P2 28 28 255\n'
            s += ' '.join(s_data)
            i_name = './mnist/{0}-{1}-{2}.pgm'.format(name, idx, label)
            with open(i_name, 'w', encoding='utf-8') as f:
                f.write(s)
    csv_f.close()
    lbl_f.close()
    img_f.close()


# 결과를 파일로 출력하기
to_csv('train', 1000)
to_csv('t10k', 500)
