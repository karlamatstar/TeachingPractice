package com.logitics.erp.employeefamily.service;

import com.logitics.erp.employeefamily.dto.EmployeeFamilyInfoRequest;
import com.logitics.erp.employeefamily.dto.EmployeeFamilyInfoResponse;
import com.logitics.erp.employeefamily.mapper.EmployeeFamilyMapper;
import com.logitics.erp.employeefamily.repository.EmployeeFamilyRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class EmployeeFamilyService {

	private final EmployeeFamilyRepository employeeFamilyRepository;
	private final EmployeeFamilyMapper employeeFamilyMapper;

	public List<EmployeeFamilyInfoResponse> getEmployeeFamilyInfo(String employeeNo) {
		return employeeFamilyMapper.getEmployeeFamilyInfo(employeeNo);
	}

	public boolean addFamiliyInfo(EmployeeFamilyInfoRequest familyInfoRequest) {
		return employeeFamilyMapper.addFamiliyInfo(familyInfoRequest) > 0;
	}

	public boolean deleteFamilyInfo(Long familyId) {
		return employeeFamilyMapper.deleteFamilyInfo(familyId) > 0;
	}
}
