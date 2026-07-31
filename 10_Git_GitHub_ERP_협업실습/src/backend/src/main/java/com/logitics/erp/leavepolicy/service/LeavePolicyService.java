package com.logitics.erp.leavepolicy.service;

import com.logitics.erp.leavepolicy.dto.LeavePolicyRequest;
import com.logitics.erp.leavepolicy.dto.LeavePolicyResponse;
import com.logitics.erp.leavepolicy.mapper.LeavePolicyMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class LeavePolicyService {
	private final LeavePolicyMapper leavePolicyMapper;

	public List<LeavePolicyResponse> getLeavePolicies() {
		return leavePolicyMapper.getLeavePolicies();
	}

	public Boolean addLeavePolicy(LeavePolicyRequest leavePolicyRequest) {
		return leavePolicyMapper.addLeavePolicy(leavePolicyRequest);
	}
}
