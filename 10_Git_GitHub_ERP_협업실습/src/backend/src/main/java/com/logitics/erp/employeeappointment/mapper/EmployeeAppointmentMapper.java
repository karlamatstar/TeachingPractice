package com.logitics.erp.employeeappointment.mapper;

import com.logitics.erp.employeeappointment.dto.AppointmentHistoryRequest;
import com.logitics.erp.employeeappointment.dto.AppointmentHistoryResponse;
import com.logitics.erp.employeeappointment.dto.EmployeementAppointmentResponse;
import com.logitics.erp.employeeappointment.dto.RegisterAppointmentRequest;
import com.logitics.erp.employeeeventsupport.dto.EmployeeEventSupportResponse;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface EmployeeAppointmentMapper {

	List<EmployeementAppointmentResponse> getEmployeeAppointmentHistory(
					@Param("size") int size,
					@Param("offset") int offset,
					@Param("keyword") String keyword
	);

	int registerAppointment(RegisterAppointmentRequest registerAppointmentRequest);

	List<EmployeeEventSupportResponse> getEventSupportList(int size, int offset, String keyword);

    List<AppointmentHistoryResponse> getAppointmentHistory(AppointmentHistoryRequest appointmentHistoryRequest);
}
