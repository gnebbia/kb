# frozen_string_literal: true

class Kb < Formula
  include Language::Python::Virtualenv

  desc "Minimalist knowledge base manager"
  homepage "https://github.com/gnebbia/kb"
  url "https://github.com/gnebbia/kb.git",
    tag:      "v0.1.5",
    revision: "7abc8f7d816ca80a7c5ef1aacd0fe20c2c1f12cf"
  license "GPL-3.0-or-later"

  depends_on "python@3.8"

  resource "attr" do
    url "https://files.pythonhosted.org/packages/de/be/ddc7f84d4e087144472a38a373d3e319f51a6faf6e5fc1ae897173675f21/attr-0.3.1.tar.gz"
    sha256 "9091548058d17f132596e61fa7518e504f76b9a4c61ca7d86e1f96dbf7d4775d"
  end

  resource "attrs" do
    url "https://files.pythonhosted.org/packages/81/d0/641b698d05f0eaea4df4f9cebaff573d7a5276228ef6b7541240fe02f3ad/attrs-20.2.0.tar.gz"
    sha256 "26b54ddbbb9ee1d34d5d3668dd37d6cf74990ab23c828c2888dccdceee395594"
  end

  resource "colored" do
    url "https://files.pythonhosted.org/packages/b2/16/04827e24c14266d9161bd86bad50069fea453fa006c3d2b31da39251184a/colored-1.4.2.tar.gz"
    sha256 "056fac09d9e39b34296e7618897ed1b8c274f98423770c2980d829fd670955ed"
  end

  resource "toml" do
    url "https://files.pythonhosted.org/packages/da/24/84d5c108e818ca294efe7c1ce237b42118643ce58a14d2462b3b2e3800d5/toml-0.10.1.tar.gz"
    sha256 "926b612be1e5ce0634a2ca03470f95169cf16f939018233a670519cb4ac58b0f"
  end

  resource "flask" do
    url "https://files.pythonhosted.org/packages/4e/0b/cb02268c90e67545a0e3a37ea1ca3d45de3aca43ceb7dbf1712fb5127d5d/Flask-1.1.2.tar.gz"
    sha256 "4efa1ae2d7c9865af48986de8aeb8504bf32c7f3d6fdc9353d34b21f4b127060"
  end

  resource "flask-httpauth" do
    url "https://files.pythonhosted.org/packages/2d/6a/e458a74c909899d136aa76cb4d707f0f600fba6ca0d603de681e8fcac91f/Flask-HTTPAuth-4.2.0.tar.gz"
    sha256 "8c7e49e53ce7dc14e66fe39b9334e4b7ceb8d0b99a6ba1c3562bb528ef9da84a"
  end

  def install
    virtualenv_install_with_resources
  end
end
