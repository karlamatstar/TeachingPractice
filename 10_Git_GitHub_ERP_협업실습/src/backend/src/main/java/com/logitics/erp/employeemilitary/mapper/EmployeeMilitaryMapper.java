package com.logitics.erp.employeemilitary.mapper;

import com.logitics.erp.employeemilitary.dto.EmployeeMilitaryInfoResponse;
import com.logitics.erp.employeemilitary.dto.EmployeeMilitaryAddInfoRequest;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface EmployeeMilitaryMapper {
	public List<EmployeeMilitaryInfoResponse> getEmployeeMilitaryInfo(@Param("employeeNo") String employeeNo);
	public int addMilitaryInfo(EmployeeMilitaryAddInfoRequest militaryAddInfoRequest);
	public int deleteMilitaryInfo(@Param("militaryId") Long militaryId);
}
