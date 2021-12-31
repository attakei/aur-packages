# Maintainer: Your Name <youremail@domain.com>
pkgname=firebase-tools-bin
pkgver=10.0.1
pkgrel=1
epoch=
pkgdesc=" The Firebase Command Line Tools (bundled official standalone binary)"
arch=('x86_64')
url="https://github.com/firebase/firebase-tools"
license=('MIT')
groups=()
depends=()
makedepends=()
checkdepends=()
optdepends=()
provides=()
conflicts=('firebase-tools')
replaces=()
backup=()
options=('!strip')
install=
changelog=
source=(
    "https://github.com/firebase/firebase-tools/releases/download/v${pkgver}/${pkgname/-bin/}-linux"
    "https://github.com/firebase/firebase-tools/raw/v${pkgver}/LICENSE"
)
noextract=()
md5sums=(
    '64dd4eb456d4cc4b60e1b9bffb051c18'
    '6ea8f4d1de9a164d33ffe95483a58af4'
)
validpgpkeys=()

package() {
    name=${pkgname/-bin/}-linux
    chmod +x ${srcdir}/${name}
    install -Dm644 "${srcdir}/LICENSE" "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
    install -Dm755 "${srcdir}/${name}" "${pkgdir}/usr/bin/firebase"
}

