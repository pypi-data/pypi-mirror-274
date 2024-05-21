# https://www.geeksforgeeks.org/how-to-generate-qr-codes-with-a-custom-logo-using-python/
import os
import qrcode
import qrcode.image.svg
from PIL import Image
# flask imports
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from http import HTTPStatus

class QRlabels:
    def __init__(
        self, app, redirect_paths, url_prefix='/labels',
        qr_logo_file='logo.png', label_image_file=None,
        info_lines=['Origin:', 'Weight:', 'Expiration date:']
    ):
        self.app = app
        self.static_dir = app.static_folder
        self.static_url = app.static_url_path
        self.redirect_paths = redirect_paths
        self.blueprint = Blueprint(
            'qrl_blueprint', __name__,
            url_prefix=url_prefix,
            template_folder='templates'
        )

        self.blueprint.add_url_rule("/", 'qrl', view_func=self.qrl_index, methods=['GET'])
        self.blueprint.add_url_rule("/qrcode/<path:qrpath>", 'qrpath', view_func=self.qr4path, methods=['GET'])
        self.blueprint.add_url_rule("/qrprint/<path:qrpath>", 'qrprint', view_func=self.make_label, methods=['GET'])
        self.blueprint.add_url_rule("/qrprints/<prefix_key>", 'qrprints', view_func=self.make_labels, methods=['GET'])
        app.register_blueprint(
            self.blueprint, url_prefix=url_prefix
        )
        self.logo_settings(qr_logo_file)
        self.label_image_url = os.path.join(self.static_url, label_image_file or qr_logo_file)
        self.info_lines = info_lines

    def logo_settings(self, logo_file):
        # Image for QR code center
        self.logo_file = os.path.join(self.static_dir, logo_file)
        self.logo = Image.open(self.logo_file)
        self.basewidth = 100

        # adjust image size
        self.wpercent = (self.basewidth/float(self.logo.size[0]))
        self.hsize = int((float(self.logo.size[1])*float(self.wpercent)))
        self.logo = self.logo.resize((self.basewidth, self.hsize), Image.LANCZOS)

        # fill transparent layer
        self.fill_color = (255,255,255)
        background = Image.new(self.logo.mode[:-1], self.logo.size, self.fill_color)
        background.paste(self.logo, self.logo.split()[-1]) # omit transparency
        self.logo = background
    
    @login_required
    def qrl_index(self):
        if current_user.role != 'admin':
            abort(HTTPStatus.UNAUTHORIZED)
        return render_template('QRlabels/index.html', redirect_paths=self.redirect_paths)

    @login_required
    def qr4path(self, qrpath):
        if current_user.role != 'admin':
            abort(HTTPStatus.UNAUTHORIZED)
        path = os.path.join(request.host_url, qrpath)
        filename = f"qr{hash(qrpath)}.svg"
        filepath = os.path.join(self.static_dir, filename)
        qrimg = self.make_qr_code(path, filepath)
        return redirect(os.path.join(self.static_url,filename))
        #TODO protected file send: https://pythonprogramming.net/flask-protected-files-tutorial/
        #return qrimg

    @login_required
    def make_label(self, qrpath): #, width=210, height=297):
        if current_user.role != 'admin':
            abort(HTTPStatus.UNAUTHORIZED)
        path = os.path.join(request.host_url, qrpath)
        filename = f"qr{hash(qrpath)}.png"
        filepath = os.path.join(self.static_dir, filename)
        qrimg = self.make_qr_code(path, filepath)
        return render_template(
            'QRlabels/label.svg', label_image=self.label_image_url, info_lines=self.info_lines,
            width=100, height=100, x_pos=0, y_pos=0, qr=os.path.join(self.static_url,filename)
        ) #qrimg

    @login_required
    def make_labels(self, prefix_key, rows=2, cols=2):
        if current_user.role != 'admin':
            abort(HTTPStatus.UNAUTHORIZED)
        prefix_path = os.path.join(request.host_url, self.redirect_paths[prefix_key])
        image_hrefs = [
            [os.path.join(self.static_url,self.make_random_path_qr(prefix_path)) for i in range(cols)]
            for i in range(rows)
        ]
        return render_template(
            'QRlabels/labels.svg', rows=rows, cols=cols,
            image_hrefs=image_hrefs, label_image=self.label_image_url,
            info_lines=self.info_lines
        )

    def make_qr_code(self, path, filename=None, host_url=None, color='Black'):
        QRcode = qrcode.QRCode(
	    error_correction=qrcode.constants.ERROR_CORRECT_H
        )

        # taking url or text
        if host_url:
            url = os.path.join(host_url, qrpath)
        else: url = path

        # adding URL or text to QRcode
        QRcode.add_data(url)

        # generating QR code
        QRcode.make()

        # adding color to QR code
        QRimg = QRcode.make_image(
	    #fill_color=color, back_color="white",
            image_factory=(
                None if (filename and filename.endswith('.png'))
                else (qrcode.image.svg.SvgImage if filename else qrcode.image.svg.SvgFragmentImage))
        )
        if filename and filename.endswith('.png'):
            QRimg = QRimg.convert('RGB')

            # set size of QR code
            pos = ((QRimg.size[0] - self.logo.size[0]) // 2,
	           (QRimg.size[1] - self.logo.size[1]) // 2)
            QRimg.paste(self.logo, pos)

            # save the QR code generated
            QRimg.save(filename)
            return filename

        elif filename and filename.endswith('.svg'):
            QRimg.save(filename)
            return filename
        else: return QRimg.to_string(encoding='unicode')

    def make_random_path_qr(self, prefix_path):
        import secrets
        qrpath = os.path.join(prefix_path,secrets.token_urlsafe(16))
        filename = f"qr{hash(qrpath)}.png"
        filepath = os.path.join(self.static_dir, filename)
        qrimg = self.make_qr_code(qrpath, filepath)
        return filename
