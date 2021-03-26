# Maintainer: Giuseppe Nebbione <nebbionegiuseppe at gmail dot com>

pkgname=python-kb-git
_reponame="kb"
pkgver=r100.b6b334f
pkgrel=1
pkgdesc="A command line minimalist knowledge base manager"
arch=(any)
url="https://github.com/gnebbia/kb.git"
license=('GPL3')
depends=()
makedepends=('git')
provides=("python-kb-git")
conflicts=("python-kb-git" "python-kb" "kb")
source=("git+$url")
md5sums=('SKIP')

pkgver() {
	cd "$srcdir/${_reponame}"
	printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
	cd "$srcdir/${_reponame}"
	python setup.py install --root="${pkgdir}/" --optimize=1
	install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

