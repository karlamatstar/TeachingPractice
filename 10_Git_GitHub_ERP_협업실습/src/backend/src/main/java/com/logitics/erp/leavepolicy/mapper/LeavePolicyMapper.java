package com.logitics.erp.leavepolicy.mapper;

import com.logitics.erp.leavepolicy.dto.LeavePolicyRequest;
import com.logitics.erp.leavepolicy.dto.LeavePolicyResponse;

import java.util.List;

public interface LeavePolicyMapper {
	List<LeavePolicyResponse> getLeavePolicies();

	Boolean addLeavePolicy(LeavePolicyRequest leavePolicyRequest);
}
