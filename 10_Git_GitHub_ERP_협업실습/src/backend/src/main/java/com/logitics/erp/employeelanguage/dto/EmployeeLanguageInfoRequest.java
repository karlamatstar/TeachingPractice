package com.logitics.erp.employeelanguage.dto;

import com.logitics.erp.employee.entity.Employee;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class EmployeeLanguageInfoRequest {
	private Long employeeLanguageId;

	private String languageName;
	private String readingLevel;
	private String writingLevel;
	private String speakingLevel;
	private String testName;
	private String testScore;
	private LocalDate issuedDate;
	private String issuer;
}
