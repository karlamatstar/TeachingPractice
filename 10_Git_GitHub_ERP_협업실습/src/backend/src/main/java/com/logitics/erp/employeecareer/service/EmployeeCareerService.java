package com.logitics.erp.employeecareer.service;

import com.logitics.erp.employeecareer.dto.EmployeeCareerAddInfoRequest;
import com.logitics.erp.employeecareer.dto.EmployeeCareerInfoResponse;
import com.logitics.erp.employeecareer.mapper.EmployeeCareerMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class EmployeeCareerService {

	private final EmployeeCareerMapper employeeCareerMapper;

	public List<EmployeeCareerInfoResponse> getEmployeeCareerInfo(Long employeeId) {
		return employeeCareerMapper.getEmployeeCareerInfo(employeeId);
	}

	public boolean addInfo(EmployeeCareerAddInfoRequest addRequest) {
		return employeeCareerMapper.addInfo(addRequest) > 0;
	}

	public boolean deleteInfo(Long deleteCareerId) {
		return employeeCareerMapper.deleteInfo(deleteCareerId) > 0;
	}


}
