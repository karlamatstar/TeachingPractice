package com.logitics.erp.employeefamily.mapper;

import com.logitics.erp.employeefamily.dto.EmployeeFamilyInfoRequest;
import com.logitics.erp.employeefamily.dto.EmployeeFamilyInfoResponse;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface EmployeeFamilyMapper {
	public List<EmployeeFamilyInfoResponse> getEmployeeFamilyInfo(@Param("employeeNo") String employeeNo);

	int addFamiliyInfo(EmployeeFamilyInfoRequest familiyInfoRequest);

	int deleteFamilyInfo(Long familyId);
}
