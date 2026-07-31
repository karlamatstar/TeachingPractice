package com.logitics.erp.employeeeventsupport.mapper;

import com.logitics.erp.employeeeventsupport.dto.EmployeeEventSupportRegisterRequest;
import com.logitics.erp.employeeeventsupport.dto.EmployeeEventSupportResponse;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface EmployeeEventSupportMapper {
	List<EmployeeEventSupportResponse> getSupportList(
					@Param("size") int size,
					@Param("offset") int offset,
					@Param("keyword") String keyword,
					@Param("employeeId") Long employeeId
	);

	int registerEventSupport(EmployeeEventSupportRegisterRequest registerRequest);

	int deleteEventSupport(Long eventSupportId);

    int updateFileRefId(Long fileId, Long eventSupportId);

    EmployeeEventSupportResponse getEventSupportDetail(Long eventSupportId);
}
