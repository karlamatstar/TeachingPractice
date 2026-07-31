package com.logitics.erp.employeecertificate.dto;

import com.logitics.erp.employee.entity.Employee;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class EmployeeCertificateInfoResponse {

	private Long employeeCertificateId;

	private String certificateName;
	private String issuingAgency;

	private LocalDate acquiredDate;
	private LocalDate expirationDate;

	private String certificateNumber;

}
