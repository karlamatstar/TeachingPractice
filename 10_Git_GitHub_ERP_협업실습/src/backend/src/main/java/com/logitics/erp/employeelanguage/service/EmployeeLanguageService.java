package com.logitics.erp.employeelanguage.service;

import com.logitics.erp.employeelanguage.dto.EmployeeLanguageInfoRequest;
import com.logitics.erp.employeelanguage.dto.EmployeeLanguageInfoResponse;
import com.logitics.erp.employeelanguage.mapper.EmployeeLanguageMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class EmployeeLanguageService {
	private final EmployeeLanguageMapper employeeLanguageMapper;

	public List<EmployeeLanguageInfoResponse> getEmployeeLanguageInfo(String employeeNo) {
		return employeeLanguageMapper.getEmployeeLanguageInfo(employeeNo);
	}

	public boolean addEmployeeLanguageInfo(EmployeeLanguageInfoRequest languageInfoRequest) {
		return employeeLanguageMapper.addEmployeeLanguageInfo(languageInfoRequest);
	}

	public boolean deleteEmployeeLanguageInfo(Long languageId) {
		return employeeLanguageMapper.deleteEmployeeLanguageInfo(languageId);
	}
}
