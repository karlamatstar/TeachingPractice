package com.logitics.erp.leavetype.service;

import com.logitics.erp.leavetype.dto.LeaveTypeResponse;
import com.logitics.erp.leavetype.mapper.LeaveTypeMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class LeaveTypeService {

	private final LeaveTypeMapper leaveTypeMapper;

	public List<LeaveTypeResponse> getLeaveType() {
		return leaveTypeMapper.getLeaveType();
	}
}
