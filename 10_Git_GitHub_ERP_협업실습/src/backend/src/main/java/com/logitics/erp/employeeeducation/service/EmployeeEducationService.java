package com.logitics.erp.employeeeducation.service;

import com.logitics.erp.employeeeducation.dto.EmployeeEducationInfoRequest;
import com.logitics.erp.employeeeducation.dto.EmployeeEducationInfoResponse;
import com.logitics.erp.employeeeducation.mapper.EmployeeEducationMapper;
import com.logitics.erp.employeeeducation.repository.EmployeeEducationRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class EmployeeEducationService {

	private final EmployeeEducationRepository employeeEducationRepository;
	private final EmployeeEducationMapper employeeEducationMapper;

	public List<EmployeeEducationInfoResponse> getEmployeeEducationInfo(String employeeNo) {
		return employeeEducationMapper.getEmployeeEducationInfo(employeeNo);
	}

	public boolean addEmployeeEducationInfo(EmployeeEducationInfoRequest educationInfoRequest) {
		return employeeEducationMapper.addEmployeeEducationInfo(educationInfoRequest) > 0;
	}

	public boolean deleteEmployeeEducationInfo(Long educationId) {
		return employeeEducationMapper.deleteEmployeeEducationInfo(educationId) > 0;
	}
}
