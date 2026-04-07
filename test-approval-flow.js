// Test script to verify the approval flow
const FIREBASE_URL = 'https://super-team-netflix-default-rtdb.europe-west1.firebasedatabase.app';

async function testFlow() {
  console.log('=== APPROVAL FLOW TEST ===\n');
  
  // Test 1: Create a test user
  console.log('1. Testing user registration...');
  const testUser = {
    name: 'Test User',
    email: 'test-' + Date.now() + '@example.com',
    phone: '1234567890',
    tab: 'Test Tab',
    status: 'pending',
    registeredAt: new Date().toISOString()
  };
  
  try {
    const res = await fetch(FIREBASE_URL + '/users.json', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(testUser)
    });
    const data = await res.json();
    console.log('✓ User created with key:', data.name);
    const userKey = data.name;
    
    // Test 2: Verify user was created
    console.log('\n2. Verifying user was created...');
    const getRes = await fetch(FIREBASE_URL + '/users/' + userKey + '.json');
    const userData = await getRes.json();
    console.log('✓ User retrieved, status:', userData.status);
    
    // Test 3: Test PATCH request (approval)
    console.log('\n3. Testing PATCH to set status to approved...');
    const patchRes = await fetch(FIREBASE_URL + '/users/' + userKey + '.json', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: 'approved' })
    });
    console.log('✓ PATCH response status:', patchRes.status);
    const patchData = await patchRes.json();
    console.log('✓ PATCH response:', patchData);
    
    // Test 4: Verify approval worked
    console.log('\n4. Verifying approval...');
    const verifyRes = await fetch(FIREBASE_URL + '/users/' + userKey + '.json');
    const verifyData = await verifyRes.json();
    console.log('✓ User status after PATCH:', verifyData.status);
    
    if (verifyData.status === 'approved') {
      console.log('\n✅ APPROVAL FLOW WORKS CORRECTLY!');
    } else {
      console.log('\n❌ APPROVAL FAILED - Status is:', verifyData.status);
    }
    
  } catch(e) {
    console.error('❌ Error:', e.message);
  }
}

testFlow();
