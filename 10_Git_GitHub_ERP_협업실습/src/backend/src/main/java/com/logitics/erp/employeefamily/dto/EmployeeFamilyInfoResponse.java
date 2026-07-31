package com.logitics.erp.employeefamily.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class EmployeeFamilyInfoResponse {

	private Long employeeFamilyId;

	private String familyName;
	private String familyRelation;
	private LocalDate birthDate;
	private String job;
	private String companyName;

	private boolean livingTogether = false;
	private boolean dependent = false;
	private boolean disabled = false;

}
