package com.logitics.erp.attendance.mapper;

import com.logitics.erp.attendance.dto.AttendResponse;
import com.logitics.erp.attendance.dto.AttendanceDailyResponse;
import com.logitics.erp.attendance.dto.AttendanceInfoListResponse;
import com.logitics.erp.attendance.dto.AttendanceResultResponse;

import java.util.List;

public interface AttendanceMapper {
	List<AttendanceResultResponse> getMonthAttendance(int size, int offset, Long departmentId, String startDate, String endDate);

	List<AttendanceDailyResponse> getAttendanceDaily(String findDate);

	List<AttendanceInfoListResponse> getAttendanceInfoList(String findDate);
}
