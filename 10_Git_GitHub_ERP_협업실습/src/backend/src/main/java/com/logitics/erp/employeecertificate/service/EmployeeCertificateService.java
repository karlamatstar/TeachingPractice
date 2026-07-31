package com.logitics.erp.employeecertificate.service;

import com.logitics.erp.employeecareer.dto.EmployeeCareerAddInfoRequest;
import com.logitics.erp.employeecareer.dto.EmployeeCareerInfoResponse;
import com.logitics.erp.employeecertificate.dto.EmployeeCertificateInfoResponse;
import com.logitics.erp.employeecertificate.mapper.EmployeeCertificateMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

import org.springframework.transaction.annotation.Transactional;

import com.logitics.erp.employeecertificate.dto.EmployeeCertificateAddInfoRequest;
import com.logitics.erp.employeecertificate.dto.EmployeeCertificateInfoResponse;

import com.logitics.erp.employeecertificate.entity.EmployeeCertificate;
@Service
@RequiredArgsConstructor
public class EmployeeCertificateService {

	private final EmployeeCertificateMapper employeeCertificateMapper;

	public List<EmployeeCertificateInfoResponse> getEmployeeCertificateInfo(Long employeeId) {
		return employeeCertificateMapper.getEmployeeCertificateInfo(employeeId);
	}

	public boolean addCertificateInfo(EmployeeCertificateAddInfoRequest addRequest) {
		return employeeCertificateMapper.addCertificateInfo(addRequest) > 0;
	}

	public boolean deleteCertificateInfo(Long deleteCareerId) {
		return employeeCertificateMapper.deleteCertificateInfo(deleteCareerId) > 0;
	}

}
