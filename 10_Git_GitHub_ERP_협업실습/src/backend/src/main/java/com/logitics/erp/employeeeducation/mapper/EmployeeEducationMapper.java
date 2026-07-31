package com.logitics.erp.employeeeducation.mapper;

import com.logitics.erp.employeeeducation.dto.EmployeeEducationInfoRequest;
import com.logitics.erp.employeeeducation.dto.EmployeeEducationInfoResponse;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface EmployeeEducationMapper {
	public List<EmployeeEducationInfoResponse> getEmployeeEducationInfo(@Param("employeeNo")String employeeNo);

	int addEmployeeEducationInfo(EmployeeEducationInfoRequest educationInfoRequest);

	int deleteEmployeeEducationInfo(Long educationId);
}
