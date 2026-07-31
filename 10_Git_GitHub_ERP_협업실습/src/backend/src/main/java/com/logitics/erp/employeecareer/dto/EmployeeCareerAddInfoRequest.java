package com.logitics.erp.employeecareer.dto;

import com.logitics.erp.employee.entity.Employee;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class EmployeeCareerAddInfoRequest {
	private Long employeeId;

	private String companyName;

	private LocalDate hireDate;
	private LocalDate resignationDate;

	private String positionName;
	private String departmentName;
	private String resignationReason;

}
