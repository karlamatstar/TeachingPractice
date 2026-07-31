package com.logitics.erp.common.advice;

import com.logitics.erp.common.util.ApiResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

	@ExceptionHandler(Exception.class)
	public ResponseEntity<ApiResponse<?>> handleException(Exception e) {

		return ResponseEntity
						.status(HttpStatus.INTERNAL_SERVER_ERROR)
						.body(
										new ApiResponse<>(
														false,
														e.getMessage(),
														null
										)
						);
	}
}
