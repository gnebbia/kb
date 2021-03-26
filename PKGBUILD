# Maintainer: Giuseppe Nebbione <giuseppenebbione at gmail dot com>

pkgbase='kb'
pkgname=('kb')
_module='kb-manager'
pkgver='0.1.6'
pkgrel=1
pkgdesc="A command line minimalist knowledge base manager"
url="https://github.com/gnebbia/kb"
depends=('python')
makedepends=('python-setuptools')
license=('GPL3')
arch=('any')
source=("https://files.pythonhosted.org/packages/source/${_module::1}/$_module/$_module-$pkgver.tar.gz")
sha256sums=('78e14f6eef30a4742925cc75ba9a5509c032ae42e73e26582cd7ed91794f41df')

build() {
    cd "${srcdir}/${_module}-${pkgver}"
    python setup.py build
}

package() {
    depends+=()
    cd "${srcdir}/${_module}-${pkgver}"
    python setup.py install --root="${pkgdir}" --optimize=1 --skip-build
}
