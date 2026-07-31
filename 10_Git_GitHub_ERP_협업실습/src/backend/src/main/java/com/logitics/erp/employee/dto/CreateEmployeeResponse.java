package com.logitics.erp.employee.dto;

import com.logitics.erp.employee.entity.Employee;
import lombok.Data;

import java.time.LocalDate;

@Data
public class CreateEmployeeResponse {

	private final Long email;
	private final Long employeeId;
	private String employeeNo;
	private String departmentName;
	private String phone;
	private String address;
	private LocalDate hireDate;

	public CreateEmployeeResponse(
					Employee e
	) {
		this.employeeId = e.getEmployeeId();
		this.employeeNo = e.getEmployeeNo();
		this.email = e.getEmployeeId();
		this.phone = e.getPhone();
		this.departmentName = e.getDepartment().getDepartmentName();
		this.address = e.getAddress();
		this.hireDate = e.getHireDate();
	}




}
