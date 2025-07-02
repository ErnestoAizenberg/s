from fastapi import HTTPException, status

# АВТОРИЗАЦИЯ

# Пользователь
UserNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

UserIdNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Отсутствует идентификатор пользователя",
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Неверная почта или пароль"
)

FailedGoogleOauthException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Google авторизация не удалась" "Попробуйте позже",
)


# ТОКЕНЫ

TokenExpiredException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")

InvalidTokenFormatException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный формат токена"
)


TokenNoFound = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Токен отсутствует в заголовке")

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный")

NoUserIdException = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найден ID пользователя")

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

TokenInvalidFormatException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Неверный формат токена. Ожидается 'Bearer <токен>'",
)


# Файлы
FileNotProvidedException = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл не передан.")

FileNameNotProvidedException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Не передано название файла."
)

FileNotFoundS3Exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Файл не найден в хранилище S3")


# Проекты
ProjectNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")

# Фонды
FundNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Фонд не найден")

# Юкасса

YookassaCallbackForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN)
