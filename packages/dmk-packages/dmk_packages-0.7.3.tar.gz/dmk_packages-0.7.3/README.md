# DMK Packages

## 패키지 배포하기(PyPI)

- [PyPI · The Python Package Index](https://pypi.org/) 회원가입 or 로그인 (테스트가 필요하다면 [TestPyPI · The Python Package Index](https://test.pypi.org/) 회원가입 or 로그인)

- [Packaging Python Projects - Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)에 자세하게 적혀있으니 읽고 따라한다.
  - 아래는 가이드 문서에서 필요한 부분을 발췌하였다.

### 패키지 배포시 참고사항

- 배포시 API token을 사용하기 위해 `$HOME/.pypirc` 파일을 아래와 같이 작성한다.

  ```
  [testpypi]
    username = __token__
    password = pypi-AgENdGVzdC5weXBpLm9yZw......
  ```

### 패키지 빌드 & 배포 & 설치 명령어 (Unix/macOS)

1. `python3 -m pip install --upgrade build`
2. `python3 -m build`
3. `python3 -m pip install --upgrade twine`
4. `python3 -m twine upload dist/*`
   - 테스트 환경에 배포하고 싶다면 `python3 -m twine upload --repository testpypi dist/*`
5. `python3 -m pip install dmk_packages`
   - 테스트 환경에서 설치하고 싶다면 `python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps dmk_packages`

## 패키지 사용하기

```python
from dmk_packages import database as db

db.get_engine("KOREAINVESTMENT_DMK")
```
