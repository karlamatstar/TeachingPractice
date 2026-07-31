package com.logitics.erp.employee.mapper;

import com.logitics.erp.employee.dto.EmployeeListResponse;
import com.logitics.erp.employee.dto.SearchEmployeeRequest;
import com.logitics.erp.employee.entity.Employee;
import org.apache.ibatis.annotations.Param;

import java.util.List;


public interface EmployeeMapper {
	List<Employee> getTest();

	List<EmployeeListResponse> getEmployees(
					@Param("size") int size,
					@Param("offset") int offset,
					@Param("request") SearchEmployeeRequest request
	);
}
