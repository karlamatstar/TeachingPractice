package com.logitics.erp.employeecertificate.mapper;

import com.logitics.erp.employeecertificate.dto.EmployeeCertificateAddInfoRequest;
import com.logitics.erp.employeecertificate.dto.EmployeeCertificateInfoResponse;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface EmployeeCertificateMapper {
	public List<EmployeeCertificateInfoResponse> getEmployeeCertificateInfo(Long employeeId);
	public int addCertificateInfo(EmployeeCertificateAddInfoRequest certificateAddInfoRequest);
	public int deleteCertificateInfo(Long careerId);
}
