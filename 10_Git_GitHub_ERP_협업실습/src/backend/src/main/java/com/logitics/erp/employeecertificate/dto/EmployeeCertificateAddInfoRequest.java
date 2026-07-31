package com.logitics.erp.employeecertificate.dto;

import java.time.LocalDate;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class EmployeeCertificateAddInfoRequest {

	private Long employeeId;

	private String certificateName;

	private String organizationName;

	private LocalDate acquisitionDate;
}